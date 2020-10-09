#include <iostream>
#include <string>
#include <cstdint>
#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <utility>

using namespace std;

#include <algorithm>

class PackageStream {
 public:
    PackageStream(std::string data, int32_t package_len): package_len_(package_len), data_(data) {}

    int32_t PackageLen() const {
        return package_len_;
    }

    int32_t ReadPackage(char* buf) {
        int32_t next_pos = min<int32_t>(data_.size(),  pos_ + PackageLen());
        int32_t len = next_pos - pos_;

        memcpy(buf, data_.c_str() + pos_, len);
        pos_ = next_pos;
        return len;
    }
 private:
    const int32_t package_len_;
    int32_t pos_ = 0;

    std::string data_;
};

class BufferedReader {
 public:
    explicit BufferedReader(PackageStream* stream) {
        this->stream = stream;
        buf = new char[stream->PackageLen()];
        package_len = stream->ReadPackage(buf);
        max_package_len = package_len;
    }


    int32_t Read(char* output_buffer, int32_t buffer_len) {
        int32_t next_pos = std::min(package_len, buffer_len);
        int32_t len = next_pos - pos_;

        while (next_pos <= buffer_len) {

            memcpy(output_buffer + pos_, buf + pos_, len);
            pos_ = next_pos;

            if (package_len != max_package_len || len == 0) {
                break;
            }

            if (buffer_len - pos_ >= package_len) {
                pos_ = next_pos + package_len;
                len += package_len;
            } else {
                package_len = stream->ReadPackage(buf + pos_);
                next_pos = package_len + pos_;
                len += next_pos - pos_;
            }
        }

        return len;
    }

 private:
    int32_t package_len;
    int32_t max_package_len;
    char* buf;
    int32_t pos_ = 0;
    PackageStream* stream;
};

int main() {
    int32_t package_len = 0;
    int32_t read_len = 0;
    int32_t expect_len = 0;
    int ok = true;
    int cur_byte = 0;

    cin >> package_len;
    string s;
    getline(cin, s);
    getline(cin, s);
    PackageStream stream(s, package_len);
    BufferedReader reader(&stream);

    while (cin >> read_len >> expect_len) {
        std::unique_ptr<char[]> buf(new char[read_len]);

        int got_len = reader.Read(buf.get(), read_len);
        if (got_len != expect_len || memcmp(buf.get(), s.c_str() + cur_byte, expect_len) != 0) {
            ok = false;
            break;
        }
        std::cout << "Ok" << std::endl;
        cur_byte += read_len;
    }

    cout << (int)ok << endl;
}