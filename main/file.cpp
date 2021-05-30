#include<string>
#include<iostream>

std::string strFun(int a){
    std::cout<<"strFun";
    a = 21;
    int auto = a;
    auto = 21;
    std::cout<<a<<std::endl;
    return "strFunReturn";
}

int main(){
    strFun(1);
    int a = 10/2;
    std::cout<<a<<std::endl;
    ////nananana
    /*
    essa
    */
}