xspan = 100;
yspan = 50;
zspan = 50;
MyEnvironment = zeros(xspan,yspan,zspan)

numtrees = 20;

p_x = randperm(xspan);
p_x = p_x(1:numtrees);
p_y = randperm(yspan);
p_y = p_y(1:numtrees);
treeheights = randi([round(zspan/3) 2*zspan], numtrees,1);

MyEnvironment = make_trees(MyEnvironment, p_x, p_y, treeheights);

image3(MyEnvironment)