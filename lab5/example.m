x = zeros(5);
x[2,2] = 2;
x[2,3] += 2;
print x;
y = x[2,2];
print y;

y = [ [1,2,3],
      [1,2,3],
      [1,2,3] ];

y[0 + 1, 1] = 4;

y = y';

B = eye(5);
C = ones(3);

N = 10;
M = 20;

for i = 1:N {
    for j = i:M {
        print i, j;
    }
}

x = -5;

print y;
print B;
print C;
print x;