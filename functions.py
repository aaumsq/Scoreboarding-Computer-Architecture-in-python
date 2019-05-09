## verilog integration for functional modules of scoreBoard

import os

def fpa(a, b):
    if float(a) < 0:
        s1 = str(1)
    else:
        s1 = str(0)
    if float(b) < 0:
        s2 = str(1)
    else:
        s2 = str(0)
    print("fpa ",a," ",b)

    c,d= str(a).split(sep='.')
    int1 = str(c)
    f1 = str(d)
    e,f = str(b).split(sep='.')
    int2 = str(e)
    f2 = str(f)
    file1 = open("fpatbb.v", "w")  # creating the tb file
    file1.write('''module fpatbb();

reg temp,s1,s2;
reg [15:0] a1,a2;
reg[31:0] b1, b2;
real int1,f1,int2,f2;
integer i,index1=-1,index2=-1,neg_index1,neg_index2;

real f;
integer in,count=9,pos = 31,ind1,ind2,flag=1;

// ieee format
reg [15:0] final1,final2;
wire [15:0] out_put;

tryFpa obj(
.a(final1),
.b(final2),
.o(out_put)
);

initial begin
      //inputs here
      s1 = 0;     int1 = 0;     f1 = 0.0672;       //a = int1+f1
      s2 = 0;     int2 = 1;     f2 = 0.45;      //b = int2+f2

      if(s1==s2)
            if(int1 + int2 + f1 + f2 >=65536) begin
                  if(!s1)
                        $display("Inf");
                  else
                        $display("-Inf");
                  $finish;
            end
end

initial begin
if(int1==0 && f1==0) begin
      if(s2) begin
            $display("-%f",int2+f2);
            $finish;
      end
      else begin
            $display("+%f",int2+f2);
            $finish;
      end
end
else if(int2==0 && f2==0) begin
      if(s1) begin
            $display("-%f",int1+f1);
            $finish;
      end
      else begin
            $display("+%f",int1+f1);
            $finish;
      end
end
end

initial begin
      in = int1;
      for(i=0;i<=15;i=i+1)    begin
            temp = in % 2;
            if(temp)
                  index1 = i;
            a1[i] = temp;
            in = in/2;
      end
      f = f1;
      for(i=31;i>=0;i=i-1) begin
            f = f * 2;
            if(f >= 1) begin
                  b1[i] = 1;
                  if(flag)
                        neg_index1 = i-32;
                  f = f - 1;
                  flag = 0;
            end
            else
                  b1[i] = 0;

      end

//for 2nd float
      in = int2;
      for(i=0;i<=15;i=i+1)    begin
            temp = in % 2;
            if(temp)
                  index2 = i;
            a2[i] = temp;
            in = in/2;
      end
      f = f2; flag = 1;
      for(i=31;i>=0;i=i-1) begin
            f = f * 2;
            if(f >= 1) begin
                  b2[i] = 1;
                  if(flag)
                        neg_index2 = i-32;
                  f = f - 1;
                  flag = 0;
            end
            else
                  b2[i] = 0;
      end

      final1[15] = s1;  final2[15] = s2;
      if(index1 == -1)
            final1[14:10] = 15 + neg_index1;
      else
            final1[14:10] = 15+index1;

      if(index2 == -1)
            final2[14:10] = 15 + neg_index2;
      else
            final2[14:10] = 15+index2;

      ind1 = index1-1;    ind2 = index2-1;

      if(index1 >= 0) begin
      while(count >= 0 && ind1>=0) begin
            final1[count] = a1[ind1];
            ind1 = ind1 - 1;
            count = count - 1;
      end
      end

      if(index1<0)
            pos = 31+neg_index1;

      while(count >= 0) begin
            final1[count] = b1[pos];
            pos = pos - 1;
            count = count - 1;
      end

      //2nd ieee
      count = 9; pos = 31;
      if(index2 >=0) begin
      while(count > 0 && ind2>=0) begin
            final2[count] = a2[ind2];
            ind2 = ind2 - 1;
            count = count - 1;
      end
      end

      if(index2 < 0)
            pos = 31+neg_index2;

      while(count >= 0) begin
            final2[count] = b2[pos];
            pos = pos - 1;
            count = count - 1;
      end
end

/*initial begin
#5;
      $display("%f",int1+f1);
      $display("%b.%b",a1,b1);
      $display("exponent: %d",final1[14:10]);
      $display("%b",final1);

      $display("%f",int2+f2);
      $display("%b.%b",a2,b2);
      $display("exponent: %d",final2[14:10]);
      $display("%b",final2);
end
*/
initial begin
#5;
    /*  $dumpfile("fpa_half_precision.vcd");
      $dumpvars(0,fpat);
//      $display("%b", obj.var1);
//      $display("%b", obj.var2);
//      $display("%b", obj.var3);
//      $display("%b", obj.var4);
//      $display("%b", obj.var5);
//      $display("%b", obj.cla_out);
//      $display("%b", obj.c3);
//      $display("%b", obj.c4);
      $display("%d", $clog2(obj.c4));
      $display("%d", obj.shift_sub);*/
      $display("%b",out_put);
end

endmodule
''')
    file1.close()  # close the tb file
    # make sure cla_adder1.v and Sample.py are in the same folder as this python script
    os.system(" iverilog tryFpa.v fpatbb.v ")  # executing this command gives us the executable "cla"
    os.system("vvp a.out>result.txt")  # direct the output to "result.txt" file

    file = open("result.txt", "r+")  # open "result.txt" file
    out = file.read()
    file.truncate(0)  # print the contents of the file(output)
    file.close()  # close the file "result.txt"
    return str(int(out))


def cla(a, b):
    # input for arg2
    file1 = open("clatb1.v", "w")  # creating the tb file
    file1.write('''module clatb1();
    reg [15:0] a, b;
    wire [16:0] out;

    cla obj(.a(a),.b(b),.out(out));

    initial begin
          a = ''' + a + ''';  b = ''' + b + ''';
    end

    initial begin
        //$dumpfile("cla_prefix_structural.vcd");
        //$dumpvars(0,cla_tb);
        $monitor("%d ",out);
    end
    endmodule
    ''')  # writing the tb file
    file1.close()  # close the tb file
    # make sure cla_adder1.v and Sample.py are in the same folder as this python script
    os.system(" iverilog -o cla cla.v clatb1.v ")  # executing this command gives us the executable "cla"
    os.system("vvp cla>result.txt")  # direct the output to "result.txt" file

    file = open("result.txt", "r+")  # open "result.txt" file
    out = file.read()
    file.truncate(0)
    # print the contents of the file(output)
    file.close()  # close the file "result.txt"
    return str(int(out))


def mul(a, b):
    file1 = open("wallacetb.v", "w")  # creating the tb file
    file1.write(''' module wallace16;
    reg[15:0] a;
    reg[15:0]  b;
    wire[31:0]  y;
    wallace  inst(
        .a(a),
    .b(b),
    .y(y)
    );
    initial begin
    a = ''' + a + ''';  b = ''' + b + ''';
    end

    initial
    begin
    //$dumpfile("wallace.vcd");
    //$dumpvars(0, wallace);
    $monitor("%d", y);
    end
    endmodule''')
    file1.close()  # close the tb file
    # make sure cla_adder1.v and Sample.py are in the same folder as this python script
    os.system(" iverilog wallace16.v wallacetb.v ")  # executing this command gives us the executable "cla"
    os.system("vvp a.out>result.txt")  # direct the output to "result.txt" file

    file = open("result.txt", "r+")  # open "result.txt" file
    out = file.read()
    file.truncate(0)  # print the contents of the file(output)
    file.close()  # close the file "result.txt"
    return str(int(out))

def fpm(a,b):
    if float(a) < 0:
        s1 = str(1)
    else:
        s1 = str(0)
    if float(b) < 0:
        s2 = str(1)
    else:
        s2 = str(0)

    c, d = str(a).split(sep='.')
    int1 = str(c)
    f1 = str(d)
    e, f = str(b).split(sep='.')
    int2 = str(e)
    f2 = str(f)
    file1 = open("fpmtbb.v", "w")  # creating the tb file
    file1.write('''module fpmtb();

    reg temp,s1,s2;
    reg [15:0] a1,a2;
    reg[31:0] b1, b2;
    real int1,f1,int2,f2;
    integer i,index1=-1,index2=-1,neg_index1,neg_index2;

    real f;
    integer in,count=9,pos = 31,ind1,ind2,flag=1;

    // ieee format
    reg [15:0] final1,final2;
    wire [15:0] out_put;

    floatmul obj(
    .a(final1),
    .b(final2),
    .o(out_put)
    );

    initial begin
          //inputs here
          s1 = 0;     int1 = 0;     f1 = 0.0672;       //a = int1+f1
          s2 = 0;     int2 = 1;     f2 = 0.45;      //b = int2+f2

          if(s1==s2)
                if(int1 + int2 + f1 + f2 >=65536) begin
                      if(!s1)
                            $display("Inf");
                      else
                            $display("-Inf");
                      $finish;
                end
    end

    initial begin
    if(int1==0 && f1==0) begin
          if(s2) begin
                $display("-%f",int2+f2);
                $finish;
          end
          else begin
                $display("+%f",int2+f2);
                $finish;
          end
    end
    else if(int2==0 && f2==0) begin
          if(s1) begin
                $display("-%f",int1+f1);
                $finish;
          end
          else begin
                $display("+%f",int1+f1);
                $finish;
          end
    end
    end

    initial begin
          in = int1;
          for(i=0;i<=15;i=i+1)    begin
                temp = in % 2;
                if(temp)
                      index1 = i;
                a1[i] = temp;
                in = in/2;
          end
          f = f1;
          for(i=31;i>=0;i=i-1) begin
                f = f * 2;
                if(f >= 1) begin
                      b1[i] = 1;
                      if(flag)
                            neg_index1 = i-32;
                      f = f - 1;
                      flag = 0;
                end
                else
                      b1[i] = 0;

          end

    //for 2nd float
          in = int2;
          for(i=0;i<=15;i=i+1)    begin
                temp = in % 2;
                if(temp)
                      index2 = i;
                a2[i] = temp;
                in = in/2;
          end
          f = f2; flag = 1;
          for(i=31;i>=0;i=i-1) begin
                f = f * 2;
                if(f >= 1) begin
                      b2[i] = 1;
                      if(flag)
                            neg_index2 = i-32;
                      f = f - 1;
                      flag = 0;
                end
                else
                      b2[i] = 0;
          end

          final1[15] = s1;  final2[15] = s2;
          if(index1 == -1)
                final1[14:10] = 15 + neg_index1;
          else
                final1[14:10] = 15+index1;

          if(index2 == -1)
                final2[14:10] = 15 + neg_index2;
          else
                final2[14:10] = 15+index2;

          ind1 = index1-1;    ind2 = index2-1;

          if(index1 >= 0) begin
          while(count >= 0 && ind1>=0) begin
                final1[count] = a1[ind1];
                ind1 = ind1 - 1;
                count = count - 1;
          end
          end

          if(index1<0)
                pos = 31+neg_index1;

          while(count >= 0) begin
                final1[count] = b1[pos];
                pos = pos - 1;
                count = count - 1;
          end

          //2nd ieee
          count = 9; pos = 31;
          if(index2 >=0) begin
          while(count > 0 && ind2>=0) begin
                final2[count] = a2[ind2];
                ind2 = ind2 - 1;
                count = count - 1;
          end
          end

          if(index2 < 0)
                pos = 31+neg_index2;

          while(count >= 0) begin
                final2[count] = b2[pos];
                pos = pos - 1;
                count = count - 1;
          end
    end

    /*initial begin
    #5;
          $display("%f",int1+f1);
          $display("%b.%b",a1,b1);
          $display("exponent: %d",final1[14:10]);
          $display("%b",final1);

          $display("%f",int2+f2);
          $display("%b.%b",a2,b2);
          $display("exponent: %d",final2[14:10]);
          $display("%b",final2);
    end
    */
    initial begin
    #5;
        /*  $dumpfile("fpa_half_precision.vcd");
          $dumpvars(0,fpat);
    //      $display("%b", obj.var1);
    //      $display("%b", obj.var2);
    //      $display("%b", obj.var3);
    //      $display("%b", obj.var4);
    //      $display("%b", obj.var5);
    //      $display("%b", obj.cla_out);
    //      $display("%b", obj.c3);
    //      $display("%b", obj.c4);
          $display("%d", $clog2(obj.c4));
          $display("%d", obj.shift_sub);*/
          $display("%b",out_put);
    end

    endmodule
    ''')
    file1.close()  # close the tb file
    # make sure cla_adder1.v and Sample.py are in the same folder as this python script
    os.system(" iverilog floatmul.v fpmtbb.v ")  # executing this command gives us the executable "cla"
    os.system("vvp a.out>result.txt")  # direct the output to "result.txt" file

    file = open("result.txt", "r+")  # open "result.txt" file
    out = file.read()
    file.truncate(0)  # print the contents of the file(output)
    file.close()  # close the file "result.txt"
    return str(int(out))


#print(fpa(str(10.34),str(12.6)))