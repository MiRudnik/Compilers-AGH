x = [ [1,2,3],
      [1,2,3,4,5],
      [1,2] ];

y = [ [1,2,3],
      [1,2,3],
      [1,2,3.0] ];

a = eye(3);
b = a';     # this should pass
b = -a;     # this should pass

a = "Hello";
b = -a;
b = a';
