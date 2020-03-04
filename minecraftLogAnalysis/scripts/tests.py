from operator import methodcaller

from scripts.utils import FtpConnection

conn = FtpConnection()

dates = conn.ftp_get_dir_files('logs/')

dates_mod = ["-".join(date.split("-", 3)[:3]) for date in dates]

# dates_mod = map(methodcaller("split", "-", 3), dates)

print(sorted(set(dates_mod)))