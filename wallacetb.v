 module wallace16;
    reg[15:0] a;
    reg[15:0]  b;
    wire[31:0]  y;
    wallace  inst(
        .a(a),
    .b(b),
    .y(y)
    );
    initial begin
    a = 16.99;  b = 12.67;
    end

    initial
    begin
    //$dumpfile("wallace.vcd");
    //$dumpvars(0, wallace);
    $monitor("%d", y);
    end
    endmodule