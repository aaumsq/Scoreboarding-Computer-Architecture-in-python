module clatb1();
    reg [15:0] a, b;
    wire [16:0] out;

    cla obj(.a(a),.b(b),.out(out));

    initial begin
          a = 5;  b = 9;
    end

    initial begin
        //$dumpfile("cla_prefix_structural.vcd");
        //$dumpvars(0,cla_tb);
        $monitor("%d ",out);
    end
    endmodule
    