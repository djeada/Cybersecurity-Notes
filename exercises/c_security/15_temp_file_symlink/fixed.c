#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    int dir = open("scratch", O_RDONLY | O_DIRECTORY | O_CLOEXEC);
    if (dir < 0) { perror("open scratch"); return 1; }
    int fd = openat(dir, "report.tmp",
                    O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW | O_CLOEXEC,
                    0600);
    close(dir);
    if (fd < 0) { perror("openat (file already exists?)"); return 1; }
    static const char report[] = "REPORT\n";
    ssize_t n = write(fd, report, sizeof report - 1);
    int close_result = close(fd);
    if (n != (ssize_t)(sizeof report - 1) || close_result != 0) return 1;
    return 0;
}
