M302 P1; disable cold extrusion checking
M82; modo de extrusao absoluta
G92 E0 ; Reseta Extrusora
G28;
G29;
G92 E0 ; Reseta Extrusora
G1 F300;

G1 X50 Y150 Z3.5 E0;
G1 X50 Y50 Z3.5  E-25;
G1 X100 Y50 Z3.5 E-37.5;
G1 X100 Y150 Z3.5 E-62.5;
G1 X150 Y150 Z3.5  E-75;
G1 X150 Y50 Z3.5 E-87.5;

G1 X50 Y150 Z3.7  E-87.5;
G1 X50 Y50 Z3.7  E-112.5;
G1 X100 Y50 Z3.7 E-125;
G1 X100 Y150 Z3.7  E-150;
G1 X150 Y150 Z3.7  E-162.5;
G1 X150 Y50 Z3.7 E175;
M104 S0 ;Turn-off hotend
