clc
close all
clear 

file=fopen('20150801as2types.txt');
Dataset=textscan(file,'%d %s %s');
fclose(file);

sequence=Dataset{1};
model=Dataset{3};

T='Transit';
C='Content';
E='Enterpise';

Transit=0;
Content=0;
Enterpise=0;

for i=1:51507
    t=strcmp(model(i),T);
    c=strcmp(model(i),C);
    e=strcmp(model(i),E);
    if t==1
        Transit=Transit+1;
    elseif c==1
        Content=Content+1;
    elseif e==1
        Enterpise=Enterpise+1;
    end
end

data=[Transit Content Enterpise];
label={'Transit ASes','Content ASes','Enterpise ASes'};

bili=data/sum(data);
baifenbi=num2str(bili'*100,'%1.2f');
baifenbi=[repmat(blanks(2),length(data),1),baifenbi,repmat('%',length(data),1)];
baifenbi=cellstr(baifenbi);

Label=strcat(label,baifenbi');
pie(data,Label)

