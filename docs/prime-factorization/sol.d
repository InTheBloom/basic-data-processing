import std;

void main () {
    auto input = File("in.txt", "r");
    auto output = File("out.txt", "w");
    int T = input.readln.chomp.to!int;
    foreach (i; 0..T) {
        int N = input.readln.chomp.to!int;
        auto buf = new int[](0);
        foreach (x; 2..N + 1) {
            if (N < 1L * x * x) break;
            while (N % x == 0) {
                N /= x;
                buf ~= x;
            }
        }
        if (1 < N) buf ~= N;

        foreach (j; 0..buf.length) {
            output.write(buf[j], j == buf.length - 1 ? '\n' : ' ');
        }
    }
}
