import hypermedia.net.*;

UDP udp;


void setup() {
  udp = new UDP(this, 6100);
  udp.log(true);
  udp.listen(true);
}

void draw() {
;
}


void receive( byte[] data, String ip, int port ) {  // <-- extended handler
  
  
  // get the "real" message =
  // forget the ";\n" at the end <-- !!! only for a communication with Pd !!!
  data = subset(data, 0, data.length-2);
  String message = new String( data );
  
  // print the result
  println( "receive: \""+message+"\" from "+ip+" on port "+port );
}
