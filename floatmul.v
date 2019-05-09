
module floatmul(a,b,o);

input [15:0] a,b;
output [15:0]o;

wire [31:0] y;
reg [4:0] x1,x2;
wire [5:0] x;
wire [4:0]z;
wire [15:0] y1,y2,o1;
integer i;
wire oflow,ifZero;

assign y1[9:0]= a[9:0];
assign y2[9:0] = b[9:0];
assign y1[15:10] = 1;
assign y2[15:10] = 1;
//assign y1[10] = 1;
//assign y2[10] = 1;

assign o[15] =a[15]+b[15] ;
assign z[4:0] = (a[14:10]-15) + (b[14:10]-15)+15;

assign y = y1*y2;
assign  o1[9:0] = y[21]==1 ? (y[10]==1 ? y[20:11]+1:y[20:11]):(y[9]==1? y[19:10]+1 : y[19:10]);   ///rounding
assign  o1[14:10]= y[21]==1?(z-15)+16 : z; //overflow
assign  ifZero = a[14:0]==0 | b[14:0]==0 ? 1:0;
assign o[14:0] = ifZero==1 ? 0:o1[14:0];
endmodule
