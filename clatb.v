module clatb;
reg [15:0] a;
reg [15:0] b;
reg clk;
wire [16:0] o;

cla inst(
.a(a),
.b(b),
.clk(clk),
.out(o)
); 

initial begin
clk = 0;
a = 10;
b = 54;
#10
a = 1;
b = 5;
#10
$finish;
end

always 
#1 clk = !clk;

initial begin
$dumpfile("clatb.vcd");
$dumpvars(0,clatb);
//$monitor("a = %d \nb = %d \no = %d \n\n	",a,b,o);
end      
always @(a&b&o) 
$monitor("a = %d \nb = %d \no = %d \n\n	",a,b,o);


endmodule