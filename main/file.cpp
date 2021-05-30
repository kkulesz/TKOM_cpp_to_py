#include<string>
#include<iostream>

std::string strFun(int a){
    std::cout<<"strFun";
    a = 21;
    auto = a;
    std::cout<<a<<std::endl;
    return "strFunReturn";
}

int main(){
    strFun(1);
}