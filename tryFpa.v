`include "cla1.v"

module invert1(input [10:0]m, output[10:0]out);
      wire [10:0]t;
      assign t = m-1;
      assign out = ~t;
endmodule



module invert(input [10:0]m, output[11:0]out);
      wire [10:0]t;
      assign t = ~m;
      assign out = t+1;
endmodule





module tryFpa(a,b,o);

input [15:0]a,b;
output [15:0]o;
wire sign,mag,equal,biga;
wire [4:0]shift,o1;
wire [10:0]shifted,t1,t2,t5,t6,x;
wire [11:0]f1,f2;
wire [16:0] temp, temp1;
wire [4:0]shift1;
reg [4:0]shft;
reg flag;
reg [10:0] tt5;
integer i;


wire [15:0] t3,t4;

assign sign = a[15]==b[15] ? 1:0;
assign equal = a[14:10]==b[14:10] ? 1:0;
assign biga = a[14:10]>b[14:10] ? 1:0;
assign shift = biga==0 ?(b[14:10]-a[14:10]):(-b[14:10]+a[14:10]);
assign o[15] = sign==1 ? a[15]:(equal==1 ? (a[9:0]>=b[9:0] ? a[15]:b[15]):(a[14:10]>=b[14:10] ? a[15]:b[15]));
assign o1 = (sign==0 & equal==1) ? 0 : (a[14:0]>b[14:0] ? a[14:10]:b[14:10]) ;
assign t1[9:0] = biga==1 ? b[9:0] : a[9:0];
assign t1[10] = 1;
assign shifted = t1>>shift;
assign t2[9:0] = biga==1 ? a[9:0] : b[9:0];
assign t2[10] = 1;

invert i1(shifted,f1);
invert i2(t2,f2); 
assign t3 = sign==1 ? shifted:(a[15]==1 ? f1 : shifted);
assign t4 = sign==1 ? t2:(b[15]==1 ? f2 : t2);

cla1 obj(t3,t4,temp);

invert1 i3(temp[10:0],t6);

assign t5 = (sign==0 && o[15]==1) ? (t6) : (temp[10:0]);
//assign tt5 = t5;
//assign shift1 = 11- $clog2(t5);
/*always @ (a|b)
begin
for(i=9;i>=0;i--)
begin
	if(t5[10]!=1 && t5[i]==1 && flag!=1)
	begin
		assign flag=1;
		assign shft=i;
	end
end
end*/
//assign shift1 = 11-shft;
assign shift1 = t5[10]?0:t5[9]?1:t5[8]?2:t5[7]?3:t5[6]?4:t5[5]?5:t5[4]?6:t5[3]?7:t5[2]?8:t5[1]?9:t5[0]?10:11;
assign o[14:10] = equal==1 ? (temp[11]==1 ? o1+1 : o1) : o1-(shift1);
assign temp1 = (temp[11] == 1 && sign==1) ? ((temp[0]==1) ? ((temp+1)>>1) : temp>>1) : temp;	
assign o[9:0] = (sign==0) ? (t5<<(shift1)) : (temp1[9:0]);
endmodule






      