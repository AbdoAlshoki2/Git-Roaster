from enum import Enum

class GithubEventEnum(Enum):
    CommitComment = "CommitCommentEvent"
    Create = "CreateEvent"
    Delete = "DeleteEvent"
    Fork = "ForkEvent"
    Gollum = "GollumEvent"
    IssueComment = "IssueCommentEvent"
    Issues = "IssuesEvent"
    Member = "MemberEvent"
    Public = "PublicEvent"
    PullRequest = "PullRequestEvent"
    PullRequestReview = "PullRequestReviewEvent"
    PullRequestReviewComment = "PullRequestReviewCommentEvent"
    PullRequestReviewThread = "PullRequestReviewThreadEvent"
    Push = "PushEvent"
    Release = "ReleaseEvent"
    Sponsorship = "SponsorshipEvent"
    Watch = "WatchEvent"
    