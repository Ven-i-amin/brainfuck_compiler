grammar brainfuck;

prog: expr* EOF;

expr: '[' expr+ ']'
    | COMMAND
    ;

COMMAND: '>' 
    | '<' 
    | '+' 
    | '-' 
    | '.' 
    | ',' 
    ;
WS: [ \t\r\n]+ -> skip;