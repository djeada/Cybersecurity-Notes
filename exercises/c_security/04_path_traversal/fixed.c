#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const char *name = argv[1];
    if (!*name || strcmp(name, ".") == 0 || strcmp(name, "..") == 0 ||
        strchr(name, '/') != NULL) {
        fputs("rejected: only a single filename is allowed\n", stderr);
        return 1;
    }
    int dir = open("notes", O_RDONLY | O_DIRECTORY | O_CLOEXEC);
    if (dir < 0) { perror("open notes"); return 1; }
    int fd = openat(dir, name, O_RDONLY | O_NOFOLLOW | O_CLOEXEC);
    close(dir);
    if (fd < 0) { perror("openat"); return 1; }
    char buffer[128];
    ssize_t n;
    while ((n = read(fd, buffer, sizeof buffer)) > 0) {
        ssize_t pos = 0;
        while (pos < n) {
            ssize_t wrote = write(STDOUT_FILENO, buffer + pos, (size_t)(n - pos));
            if (wrote <= 0) { close(fd); return 1; }
            pos += wrote;
        }
    }
    close(fd);
    return n < 0 ? 1 : 0;
}
