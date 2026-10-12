// Exact degree-five Bernstein verification on a three-dimensional cube.
// This file contains no floating-point arithmetic. See Section 6 of the note.
#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Z = boost::multiprecision::cpp_int;
constexpr int D = 5;
constexpr int N = 216;

int choose(int n, int k) {
    if (k < 0 || k > n) return 0;
    int result = 1;
    for (int j = 1; j <= k; ++j) result = result * (n-j+1) / j;
    return result;
}
int id(int i, int j, int k) { return 36*i + 6*j + k; }

struct Box {
    std::array<Z, N> b;
    Z den;
    std::array<long long, 3> pos{};
    std::array<int, 3> lev{};
    int depth = 0;
};
struct RationalBound {
    Z numerator;
    long long denominator;  // Strictly positive in every construction below.
};
bool less(const RationalBound& a, const RationalBound& b) {
    Z left = a.numerator;
    left *= b.denominator;
    Z right = b.numerator;
    right *= a.denominator;
    return left < right;
}

// Decide whether a slope exists with b_i >= target + slope*s_i.
// side=-1 requires slope<=0 (the included half-space); side=1 requires >=0.
// Both b and s have common positive scales. These merely rescale the slope.
bool affine_test(const Box& box, const std::array<long long, N>& s,
                 int target, int side) {
    bool has_lower = side > 0, has_upper = side < 0;
    RationalBound lower{0, 1}, upper{0, 1};
    for (int i = 0; i < N; ++i) {
        Z v = box.b[i];
        if (target) v -= box.den;
        if (s[i] == 0) {
            if (v < 0) return false;
        } else if (s[i] < 0) {
            RationalBound candidate{-v, -s[i]};
            if (!has_lower || less(lower, candidate)) {
                lower = candidate;
                has_lower = true;
            }
        } else {
            RationalBound candidate{v, s[i]};
            if (!has_upper || less(candidate, upper)) {
                upper = candidate;
                has_upper = true;
            }
        }
        if (has_lower && has_upper && less(upper, lower)) return false;
    }
    return true;
}

// Exact midpoint subdivision: multiply the shared denominator by 2^5.
std::pair<Box, Box> divide(const Box& parent, int axis) {
    Box left, right;
    left.den = right.den = parent.den * 32;
    left.pos = right.pos = parent.pos;
    left.lev = right.lev = parent.lev;
    left.depth = right.depth = parent.depth + 1;
    left.pos[axis] *= 2;
    right.pos[axis] = right.pos[axis] * 2 + 1;
    ++left.lev[axis];
    ++right.lev[axis];
    for (int u = 0; u < 6; ++u) for (int v = 0; v < 6; ++v) {
        std::array<Z, 6> line;
        for (int k = 0; k < 6; ++k)
            line[k] = parent.b[axis==0 ? id(k,u,v) : axis==1 ? id(u,k,v) : id(u,v,k)];
        for (int i = 0; i < 6; ++i) {
            Z a = 0, b = 0;
            for (int j = 0; j <= i; ++j)
                a += line[j] * (choose(i,j) * (1 << (5-i)));
            for (int j = i; j < 6; ++j)
                b += line[j] * (choose(5-i,j-i) * (1 << i));
            int index = axis==0 ? id(i,u,v) : axis==1 ? id(u,i,v) : id(u,v,i);
            left.b[index] = std::move(a);
            right.b[index] = std::move(b);
        }
    }
    return {std::move(left), std::move(right)};
}

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("usage: check_cube input");
        std::ifstream in(argv[1]);
        if (!in) throw std::runtime_error("missing input");
        std::string format;
        in >> format;
        if (format != "N3-BERNSTEIN-5-V1") throw std::runtime_error("schema");
        long long tn = 0, td = 0;
        in >> tn >> td;
        if (!in || td <= 0 || td > 100000) throw std::runtime_error("threshold");
        if (Z(2)*tn < -Z(7)*td || Z(2)*tn > Z(3)*td)
            throw std::runtime_error("threshold scope");

        unsigned long long count = 0, leaves = 0;
        int max_depth = 0;
        // All ordered triples have one of these four sign patterns.
        for (int part = 0; part < 4; ++part) {
            std::array<int, 3> origin{};
            for (int i = 0; i < 3; ++i) {
                in >> origin[i];
                if (!in) throw std::runtime_error("truncated origin");
                if (origin[i] != (i < 3-part ? -7 : 0))
                    throw std::runtime_error("orthant coverage");
            }
            Box root;
            in >> root.den;
            if (root.den <= 0) throw std::runtime_error("denominator");
            for (auto& value : root.b) in >> value;
            if (!in) throw std::runtime_error("truncated coefficients");
            std::vector<Box> stack;
            stack.push_back(std::move(root));

            while (!stack.empty()) {
                Box box = std::move(stack.back());
                stack.pop_back();
                ++count;
                max_depth = std::max(max_depth, box.depth);
                if (count > 4000000 || box.depth > 95)
                    throw std::runtime_error("unresolved positivity");
                int level = *std::max_element(box.lev.begin(), box.lev.end());
                if (level > 35) throw std::runtime_error("dyadic depth");
                long long scale = 1LL << level;
                std::array<long long, 3> lower, width, upper;
                for (int i = 0; i < 3; ++i) {
                    width[i] = 7 * (1LL << (level-box.lev[i]));
                    lower[i] = origin[i]*scale + box.pos[i]*width[i];
                    upper[i] = lower[i] + width[i];
                }
                // Discard only boxes having no point with x_1<=x_2<=x_3.
                if (lower[0] > upper[1] || lower[1] > upper[2] || lower[0] > upper[2])
                    continue;
                long long sum_lower = lower[0]+lower[1]+lower[2];
                long long sum_upper = upper[0]+upper[1]+upper[2];
                Z minimum = *std::min_element(box.b.begin(), box.b.end());
                bool accepted = false;
                if (Z(sum_upper)*td <= Z(tn)*scale) {
                    accepted = minimum >= box.den;
                } else if (Z(sum_lower)*td > Z(tn)*scale) {
                    accepted = minimum >= 0;
                } else {
                    std::array<long long, N> s;
                    for (int i=0; i<6; ++i) for (int j=0; j<6; ++j) for (int k=0; k<6; ++k) {
                        Z value = Z(5*sum_lower + width[0]*i + width[1]*j + width[2]*k)*td
                                  - Z(5)*tn*scale;
                        if (value >= std::numeric_limits<long long>::max() ||
                            value <= std::numeric_limits<long long>::min())
                            throw std::runtime_error("integer coordinate range");
                        s[id(i,j,k)] = value.convert_to<long long>();
                    }
                    accepted = affine_test(box, s, 1, -1) &&
                               (minimum >= 0 || affine_test(box, s, 0, 1));
                }
                if (accepted) {
                    ++leaves;
                    continue;
                }
                int axis = std::min_element(box.lev.begin(), box.lev.end()) - box.lev.begin();
                auto children = divide(box, axis);
                stack.push_back(std::move(children.second));
                stack.push_back(std::move(children.first));
            }
        }
        std::string extra;
        if (in >> extra) throw std::runtime_error("extra data");
        std::cout << "ACCEPTED_EXACT_CUBES " << count << ' ' << leaves << ' ' << max_depth << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "REJECTED: " << error.what() << '\n';
        return 1;
    }
}
