x = 0;
y = zeros(5);
z = x + y;

x = eye(5);
y = eye(8);
z = x + y;

x = [ 1,2,3,4,5 ];
y = [ [1,2,3,4,5],
      [1,2,3,4,5] ];
a = x[1];       # this should pass
a = y[1,1];     # this should pass
z = x + y;

x += y;

x = zeros(5);
y = zeros(5,7);
z = x + y;

x = ones(3.5);
z = x[7,10];
z = x[3.5,4];
v = x[2,3,4];