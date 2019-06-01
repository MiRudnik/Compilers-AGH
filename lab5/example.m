N = 10;
M = 20;

for i = 1:N {
    for j = i:M {
        if(j == 10) continue;
        print i, j; # prints numbers from i to 15 skipping 10
        if(j == 15) break;
    }
}

X = zeros(5);
X[2,2] = 2;
X[2,3] += 2;
print "X:";
print X;
y = X[2,2];
print y;

Y = [ [1,2,3],
      [1,2,3],
      [1,2,3] ];

a = -4;
Y[0 + 1, 1] = -a;
print "Y:";
print Y;

Y = Y';
print "Y Transposed";
print Y;

A = eye(5);
print "Eye (A)";
print A;

B = ones(3);
print "Ones (B)";
print B;

C = A + A;
print "eye + eye (C)";
print C;
C = A .+ A;
print "Same as above";
print C;

D = X .* A;
print "Element-wise multiplication(D = X .* A)";
print D;

E = X * A;
print "Matrix multiplication(E = X * A)";
print E;

F = [ [1,2],
      [3,4],
      [5,6]];

G = [ [1,2,3],
      [4,5,6] ];

H = F * G;
print "[3x2] * [2x3] = [3x3]";
print F;
print G;
print H;

F *= G;
print "Same but using '*='";
print F;
