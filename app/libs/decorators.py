import functools

def login_verification(fuc):
    @functools.wraps(fuc)
    def wapper(self, *args, **kwargs):
        if not self.current_user:
            self.redirect("/login/")
            return
        return fuc(self, *args, **kwargs)
    return wapper