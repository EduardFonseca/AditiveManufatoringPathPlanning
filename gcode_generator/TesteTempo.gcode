M302 P1; disable cold extrusion checking
M82; modo de extrusao absoluta
G92 E0 ; Reseta Extrusora
G28 X Y;
G92 E0 ; Reseta Extrusora
G1 F300;
G1 E-100;
G1 E-200;
G1 E-300;
G1 E-400;
G1 E-500;
G1 E-600;
G1 E-700;
G1 E-800;
G1 E-900;
M104 S0 ;Turn-off hotend
