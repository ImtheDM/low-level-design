#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

using namespace std;

mutex resourceA;
mutex resourceB;

void func1() {
    unique_lock<mutex> lockA(resourceA);
    cout << "Executing func1..." << endl;
    this_thread::sleep_for(chrono::milliseconds(50));
    cout << "Fetching lock b" << endl;

    unique_lock<mutex> lockB(resourceB);
    cout << "Got both locks, exec completed" << endl;

    cout << "func1 completed" << endl;
}

void func2() {
    unique_lock<mutex> lockB(resourceB);
    cout << "Executing func2..." << endl;
    this_thread::sleep_for(chrono::milliseconds(50));
    cout << "Fetching lock a" << endl;

    unique_lock<mutex> lockA(resourceA);
    cout << "Got both locks, exec completed" << endl;

    cout << "func2 completed" << endl;
}

int main() {
    thread t1(func1);
    thread t2(func2);

    t1.join();
    t2.join();

    cout << "Execution Completed" << endl;
    return 0;
}
