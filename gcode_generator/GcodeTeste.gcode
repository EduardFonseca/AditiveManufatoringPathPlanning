M302 P1; disable cold extrusion checking
M82; modo de extrusao absoluta
G92 E0 ; Reseta Extrusora
G28 X Y;
G92 E0 ; Reseta Extrusora
G1 F1000;
G1 X0 Y200 E0;
G1 X200 Y200 E-50;
M104 S0 ;Turn-off hotend
