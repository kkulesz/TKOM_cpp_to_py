#include<string>

std::string strFun(int a){
    std::cout<<"strFun"<<std::endl;
    return "strFunReturn";
}

int main(){
    int i = 0;
    while( i<10 ){
        std::cout<<i<<std::endl;
        strFun(i);
        i = i + 1;
    }
    std::cout<<false<<std::endl;
}