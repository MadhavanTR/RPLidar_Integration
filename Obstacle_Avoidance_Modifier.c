char x,xs[2];
char xd[10];
char yd[10];
int count=0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    x=Serial.read();
    xs[2]=x;
    Serial.println(x);
    if(count%2==0)
      strcat(xd,xs);
    else
      strcat(yd,xs);
    if(x=='.'){
      if(Serial.available()){
        x=Serial.read();
        xs[2]=x;
        Serial.println(x);
        if(count%2==0)
        strcat(xd,xs);
        else
        strcat(yd,xs);
      }
      if(Serial.available()){
        x=Serial.read();
        Serial.println(x);
        Serial.println(xd);
        xs[2]=x;
        if(count%2==0){
          strcat(xd,xs);
          Serial.println(xd);}
        else{
          strcat(yd,xs);
    //send xd,yd here:
          //Serial.println(xd);
          //Serial.println(yd);
   // for(int i=0;i<strlen(xd);i++)
   //   xd[i]="\0";
   // for(int i=0;i<strlen(yd);i++)
   //   yd="";
          strcpy(xd,"");
          strcpy(yd,"");
  }}
  count++;
  }
}
}