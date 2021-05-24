#include<string>

std::string funTwoArgs(bool b, std::string s){
    return "";
}

bool funOneArg(int a){
    return false;
}

int funNoArgs(){
    std::cout<<"nananananana"<<std::endl;
}

int main(){
    std::cout<<"napis"<<std::endl;
    funNoArgs();
    funOneArg(21+232);
    funTwoArgs(true, "nanana");
    return 0;
}