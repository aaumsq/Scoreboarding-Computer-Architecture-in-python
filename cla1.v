module cla1(input [15:0]a, input [15:0]b,output [16:0]out);
reg [16:0]out;
integer i;
wire [1:0]w[0:16], x1[0:15], x2[0:15], x3[0:15], x4[0:15];
wire L5[15:0];
genvar q;
generate    
   for(q=0; q<=15; q=q+1) begin
    stat s(.a(a[q]),.b(b[q]),.t(w[q+1]));
   end
endgenerate
assign w[0] = 0;

generate    
	for(q=0;q<=14;q=q+1) begin
	  la l(.s(w[15-q]),.f(w[14-q]),.o(x1[q]));
    end
endgenerate

assign x1[15] = w[0];

generate    
   for(q=0;q<=13;q=q+1) begin
     la l(.s(x1[q]),.f(x1[q+2]),.o(x2[q]));
   end
endgenerate

assign x2[14] = x1[14];
assign x2[15] = x1[15];

generate    
   for(q=0;q<=11;q=q+1) begin
     la l(.s(x2[q]),.f(x2[q+4]),.o(x3[q]));
   end
endgenerate

assign {x3[12], x3[13], x3[14], x3[15]} = {x2[12], x2[13], x2[14], x2[15]};

generate    
   for(q=0;q<=7;q=q+1) begin
      la l(.s(x3[q]),.f(x3[q+8]),.o(x4[q]));
    end
endgenerate

generate    
  for(q=8;q<=15;q=q+1) begin
    assign x4[q] = x3[q];
  end
endgenerate

generate    
  for(q=0;q<=15;q=q+1) begin
    assign L5[q] = a[q] ^ b[q] ^ x4[15-q][0];
  end
endgenerate

always @(*) begin
   for(i=0; i<=15; i=i+1) begin
     out[i] = L5[i];
   end
     out[16] = w[0];
end
endmodule

module stat(input a,input b,output [1:0]t);
      assign {t[0],t[1]} = {a || b , a && b};
endmodule

module la(input [1:0]s, input [1:0]f,output [1:0]o);
wire [1:0]o;
      assign o[1] = (s[1] & s[0] & !f[1]) | (s[0] & f[1] & f[0]);
      assign o[0] = (s[1] & s[0] & !f[1] & !f[0]) | (f[0] & s[0]);
endmodule
