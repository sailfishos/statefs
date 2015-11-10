#include <metafuse.hpp>
#include <cor/error.hpp>
#include <sys/time.h>

namespace metafuse
{

struct timespec DefaultTime::get_now()
{
    struct timespec now;
    auto res = clock_gettime(CLOCK_REALTIME, &now);
    if (res == -1)
        throw cor::CError(errno, "Can't get time");
    return std::move(now);
}

int DefaultTime::update_time(int mask)
{
    auto now = get_now();
    if (mask & change_time_bit)
        change_time_ = now;

    if (mask & modification_time_bit)
        modification_time_ = now;

    if (mask & access_time_bit)
        access_time_ = now;

    return 0;
}

int DefaultTime::timeattr(struct stat *buf)
{
    buf->st_ctim = change_time_;
    buf->st_atim = access_time_;
    buf->st_mtim = modification_time_;
    return 0;
}

}
