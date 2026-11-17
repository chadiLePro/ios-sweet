"""Append an optional independent RO var entry without changing the root wire."""
def transform(text):
    old='    return SYSCTL_OUT(req, &entry, sizeof(entry));'
    if text.count(old)!=1 or 'a52q_data_fstab' in text:
        raise ValueError('root fstab source drift or already transformed')
    return text.replace(old,
        '    int error=SYSCTL_OUT(req, &entry, sizeof(entry));\n'
        '    if (error) return error;\n'
        '    extern int a52q_data_fstab(struct sysctl_req *);\n'
        '    return a52q_data_fstab(req);')
