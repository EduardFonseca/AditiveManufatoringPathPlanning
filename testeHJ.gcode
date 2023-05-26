M302 P1; disable cold extrusion checking
M82; modo de extrusao absoluta
G92 E0 ; Reseta Extrusora
G28;
G29; Auto bed leveling
G92 E0 ; Reseta Extrusora
F500;
G1 X100 Y50 Z3.5 E0;
G1 X100 Y150 Z3.5 E-25;