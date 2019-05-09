`include "cla32.v"

module fadd(in1,in2,in3,sum,cout);
input in1,in2,in3;
output sum,cout;
assign sum=in1^in2^in3;
assign cout=(in1&in2)|(in2&in3)|(in1&in3);
endmodule

module pp(q1,q2,q3,w1,w2);
input [31:0] q1,q2,q3;
output [31:0] w1,w2;
genvar r;
generate
for(r=0;r<31;r=r+1)
begin
fadd obj(q1[r],q2[r],q3[r],w1[r],w2[r+1]);
end
endgenerate
assign w2[0] =0;
assign w1[31] = q1[31] ^ q2[31] ^ q3[31];
endmodule

module wallace(a,b,y);
input [15:0] a,b;
output [31:0] y;
wire [31:0] u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12,u13,u14;
wire [31:0] v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14;
reg [31:0] q [15:0];

integer i,j;
always @(a or b) begin
for(i=0;i<16;i=i+1)
begin
q[i] = 0;
end
end

integer k=0;
always @( a or b) begin
for(i=0;i<16;i=i+1)
begin
for(j=0;j<16;j=j+1)
begin
q[i][j+k]=b[i] & a[j];
end
k = k+1;
end
end

pp obj1(q[0],q[1],q[2],u1,v1);
pp obj2(q[3],q[4],q[5],u2,v2);
pp obj3(q[6],q[7],q[8],u3,v3);
pp obj4(q[9],q[10],q[11],u4,v4);
pp obj5(q[12],q[13],q[14],u5,v5);

pp obj6(u1,v1,u2,u6,v6);
pp obj7(v2,u3,v3,u7,v7);
pp obj8(u4,v4,u5,u8,v8);

pp obj9(u6,v6,u7,u9,v9);
pp obj10(v7,u8,v8,u10,v10);

pp obj11(u9,v9,u10,u11,v11);
pp obj12(v10,v5,q[15],u12,v12);

pp obj13(u11,v11,u12,u13,v13);

pp obj14(u13,v13,v12,u14,v14);
assign y = u14+v14;

endmodule