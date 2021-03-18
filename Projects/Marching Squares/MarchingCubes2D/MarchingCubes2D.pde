int res = 10;
int col, row;
float surfaceLevel = 0.5;
float[][] vals;
int a, b, c, d;
float xoff = 0f; 
float yoff = 0f;
float increment = 0.1f;


void setup()
{
 size(1000, 1100);
 background(100, 120, 100);
 
 col = floor(width/res) +1;
 row = floor(height/res) +1;
 vals = new float[row][col];

 // Initalize 2d scalar field with Perlin Noise values
 for(int i = 0; i < row; i++)
 {
   xoff += increment;
   yoff = 0f;
   for(int j = 0; j < col; j++)
   {
     yoff += increment;
     vals[i][j] = noise(xoff, yoff);

 }
 
 }
 noLoop();
}

void draw()
{
  // Draw each point in the scalar field
  for(int i = 0; i < row; i++)
 {
   for (int j = 0; j < col; j++)
   {
     stroke(vals[i][j]*255);
     strokeWeight(res*0.4);
     point(i*res, j*res); 
   }
 }
 
 // Apply the marching squares algorithm to each cell in the scalar field
 delay(10);
 for(int i = 0; i < row -1; i++)
 {
  for(int j = 0; j < col -1; j++)
  {
    // i*res j*res is the coordinats of a
    a = 0; if (vals[i][j] < surfaceLevel); else a = 1;
    b = 0; if (vals[i+1][j] < surfaceLevel); else b = 1;
    c = 0; if (vals[i+1][j+1] < surfaceLevel); else c = 1;
    d = 0; if (vals[i][j+1] < surfaceLevel); else d = 1;

    drawLine(a + b * 2 + c * 4 + d * 8, i, j);
  }
 }
}

void line(PVector point1, PVector point2){
  line(point1.x, point1.y, point2.x, point2.y);
}

void drawLine(int type, int x, int y)
{
  // Create a new point for each point in the square
  Point a = new Point((x*res), (y*res), vals[x][y]);
  Point b = new Point((x*res)+res, (y*res), vals[x+1][y]);
  Point c = new Point((x*res)+res, (y*res)+res, vals[x+1][y+1]);
  Point d = new Point((x*res), (y*res)+res, vals[x][y+1]);
  
  strokeWeight(1);
  stroke(255, 0, 0);
  
  // Determine the case and draw lines accordingly 
  switch(type)
  {
  case 0:
    break;
  case 1:
    line(InterpolatePoints(a, b), InterpolatePoints(d, a));
    break;    
  case 2:
    line(InterpolatePoints(a, b), InterpolatePoints(b, c));
    break; 
  case 3:
    line(InterpolatePoints(d, a), InterpolatePoints(b, c));
    break;
  case 4:
    line(InterpolatePoints(b, c), InterpolatePoints(c, d));
    break;
  case 5:
    line(InterpolatePoints(a, b), InterpolatePoints(d, a));
    line(InterpolatePoints(b, c), InterpolatePoints(c, d));
    break;    
  case 6:
    line(InterpolatePoints(a, b), InterpolatePoints(c, d));
    break; 
  case 7:
    line(InterpolatePoints(c, d), InterpolatePoints(d, a));
    break;
  case 8:
    line(InterpolatePoints(c, d), InterpolatePoints(d, a));
    break;
  case 9:
    line(InterpolatePoints(a, b), InterpolatePoints(c, d));
    break;    
  case 10:
    line(InterpolatePoints(d, a), InterpolatePoints(c, d));
    line(InterpolatePoints(a, b), InterpolatePoints(b, c));
    break; 
  case 11:
    line(InterpolatePoints(b, c), InterpolatePoints(c, d));
    break;
  case 12:
    line(InterpolatePoints(b, c), InterpolatePoints(d, a));
    break;
  case 13:
    line(InterpolatePoints(a, b), InterpolatePoints(b, c));
    break;
  case 14:
    line(InterpolatePoints(a, b), InterpolatePoints(d, a));
    break;
  case 15:
    break;
  }
  
}

PVector InterpolatePoints(Point vertex1, Point vertex2){
  PVector edgePoint = new PVector(0, 0);
  
  // interpolate the positions of the line and draw the line
  float mu = (surfaceLevel - vertex1.value) / (vertex2.value - vertex1.value);
  edgePoint.x = vertex1.x + mu * (vertex2.x - vertex1.x);
  edgePoint.y = vertex1.y + mu * (vertex2.y - vertex1.y);
  return edgePoint;
  
}

class Point {
 float x;
 float y;
 float value;
 Point(float _x, float _y, float _value){
   x = _x;
   y = _y;
   value = _value;
 }
}
