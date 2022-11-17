M302 P1; disable cold extrusion checking
M82; modo de extrusao absoluta
G92 E0 ; Reseta Extrusora
G28 X Y;
G92 E0 ; Reseta Extrusora
G1 F1000;
G1 X50 Y150 E0;
G1 X50 Y50 E-25;
G1 X100 Y50 E-37.5;
G1 X100 Y150 E-62.5;
G1 X150 Y150 E-75;
G1 X150 Y50 E-87.5;
M104 S0 ;Turn-off hotend
