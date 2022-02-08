from github import Github
import os

class github_store:
    def __init__(self,file_path=None):
        if file_path == None:
            self.file_path = "chat_log.txt"
        self.token = os.getenv("GITHUB_TOKEN")
        self.github_object = Github(self.token)
        self.branch = "main"
        self.repository = self.github_object.get_repo("marsha-nicky/my_knowledge")
    
    def pull_data(self):
        contents = self.repository.get_contents(self.file_path, ref=self.branch)
        return contents.decoded_content.decode()

    def push(self,path=None, message=None, content=None, branch=None, update=False):

        if path == None:
            path = self.file_path
        if message == None:
            message = "Added chat knowledge"
        if content == None:
            content = self.data
        if branch == None:
            branch = self.branch

        source = self.repository.get_branch(branch)
        if update:  # If file already exists, update it
            contents = self.repository.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
            self.repository.update_file(contents.path, message, content, contents.sha, branch=branch)  # Add, commit and push branch
            print("github_storage : updated content")
        else:  # If file doesn't exist, create it
            self.repository.create_file(path, message, content, branch=branch)  # Add, commit and push branch

