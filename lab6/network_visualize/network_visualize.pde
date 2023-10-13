import hypermedia.net.*;

UDP udp;
float bgAlpha = 1.0;

PGraphics pg;

void setup() {
  udp = new UDP(this, 6100);
  //udp.log(true);
  udp.listen(true);
  
  size(200, 200);
  pg = createGraphics(width, height);
}

void draw() {
  pg.beginDraw();
  pg.background(66, 135, 245);
  pg.fill(189, 116, 237, bgAlpha);
  pg.square(0, 0, width);
  pg.fill(173, 255, 135, bgAlpha);
  pg.circle(width/2, width/2, width);
  pg.endDraw();
  
  image(pg, 0, 0);
  println(bgAlpha);
}


void receive( byte[] data, String ip, int port ) {
  
  String message = new String( data );
  bgAlpha = int(message)/4095.0*255;
  // print the result
  println( "receive: \""+message+"\" from "+ip+" on port "+port );
}
