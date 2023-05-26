M302 P1; disable cold extrusion checking
M82; modo de extrusao absoluta
G92 E0 ; Reseta Extrusora
G28 X Y;
G92 E0 ; Reseta Extrusora
G1 F100;
G1 E-100;
G1 F200;
G1 E-200;
M104 S0 ;Turn-off hotend
