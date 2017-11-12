clc
clear all

file=fopen('20170901.as-rel2.txt');
Dataset=textscan(file,'%d|%d|%d|%s'); 
fclose(file);

ASes_F=Dataset{1};
ASes_S=Dataset{2};

ASes_S=sort(ASes_S);
Link=Dataset{3};
n=length(ASes_F);
AS_1=unique(ASes_F);
AS_2=unique(ASes_S);
m=length(AS_2);

i=1;
j=1;
num=0;
number_1=zeros(n,1);
number_2=zeros(n,1);

while i<n+1
    if ASes_F(i)==AS_1(j)
        for a=i:n
            if ASes_F(a)==AS_1(j)
                num=num+1;
            else
                break;
            end
        end
        i=i+num;
        number_1(j)=num;
        j=j+1;
    else
        i=i+1;
    end
    num=0;
end

i=1;
j=1;
num=0;

while i<n+1
    if ASes_S(i)==AS_2(j)
        for a=i:n
            if ASes_S(a)==AS_2(j)
                num=num+1;
            else
                break;
            end
        end
        i=i+num;
        number_2(j)=num;
        j=j+1;
    else
        i=i+1;
    end
    num=0;
end

number_1(number_1==0)=[];
number_2(number_2==0)=[];
number_3=number_1;
number_4=number_2;

for i=1:384343
    for j=1:m
        if AS_1(i)==AS_2(j)
            number_1(i)=number_1(i)+number_2(j);
            number_2(j)=0;
            AS_2(j)=0;
        end
    end
end

number_2(number_2==0)=[];
AS_2(AS_2==0)=[];
number=cat(1,number_1,number_2);
AS=cat(1,AS_1,AS_2);
nm=length(number);
bar_P=zeros(6,1);

for i=1:nm
    if number(i)==1
        bar_P(1)=bar_P(1)+1;
    elseif number(i)>1 && number(i)<6
        bar_P(2)=bar_P(2)+1;
    elseif number(i)>5 && number(i)<101
        bar_P(3)=bar_P(3)+1;
    elseif number(i)>100 && number(i)<201
        bar_P(4)=bar_P(4)+1;
    elseif number(i)>200 && number(i)<1001
        bar_P(5)=bar_P(5)+1;
    elseif number(i)>1000
        bar_P(6)=bar_P(6)+1;
    end
end

b=bar(bar_P);
grid on;
set(0,'defaulttextinterpreter','latex'); 
set(0,'defaultlinelinewidth',2); 
set(0,'DefaultLineMarkerSize',10);
set(0,'DefaultTextFontSize', 16);
set(0,'DefaultAxesFontSize',16);
legend('XX');
xlabel('x axis');
ylabel('y axis');


            
