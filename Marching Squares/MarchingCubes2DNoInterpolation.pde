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
 size(600, 600);
 background(100, 120, 100);
 
 col = floor(width/res) +1;
 row = floor(height/res) +1;
 vals = new float[row][col];

 for(int i = 0; i < col; i++)
 {
   xoff += increment;
   yoff = 0f;
   for(int j = 0; j < row; j++)
   {
     yoff += increment;
     vals[i][j] = noise(xoff, yoff);

 }
 
 }
 noLoop();
}

void draw()
{
  for(int i = 0; i < row; i++)
 {
   for (int j = 0; j < col; j++)
   {
     stroke(vals[i][j]*255);
     strokeWeight(res*0.4);
     point(i*res, j*res); 
   }
 }
 
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
    //a = vals[i][j];
    //b = vals[i+1][j];
    //c = vals[i+1][j+1];
    //d = vals[i][j+1];
    //print(str(a + b * 2 + c * 4 + d * 8), '\n');
    drawLine(a + b * 2 + c * 4 + d * 8, i, j);
    //drawLine(1, i, j);
  }
 }
}

void line(PVector point1, PVector point2){
  line(point1.x, point1.y, point2.x, point2.y);
}

void drawLine(int type, int x, int y)
{
  PVector a = new PVector((x*res)+res*0.5, (y*res)); //
  PVector b = new PVector((x*res)+res, (y*res)+res*0.5); //
  PVector c = new PVector((x*res)+res*0.5, (y*res)+res);
  PVector d = new PVector((x*res), (y*res)+res*0.5); // 
    
  
  strokeWeight(1);
  stroke(255, 0, 0);

  switch(type)
  {
  case 0:
    break;
  case 1:
    line(a, d);
    break;    
  case 2:
    line(a, b);
    break; 
  case 3:
    line(d, b);
    break;
  case 4:
    line(b, c);
    break;
  case 5:
    line(a, d);
    line(b, c);
    break;    
  case 6:
    line(a, c);
    break; 
  case 7:
    line(c, d);
    break;
  case 8:
    line(c, d);
    break;
  case 9:
    line(a, c);
    break;    
  case 10:
    line(d, c);
    line(a, b);
    break; 
  case 11:
    line(b, c);
    break;
  case 12:
    line(b, d);
    break;
  case 13:
    line(a, b);
    break;
  case 14:
    line(a, d);
    break;
  case 15:
    break;
  }
  
  
}
