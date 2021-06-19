# Minimax algorithm

This is a minimax algorithm demo over the connect-4 and tic-tac-toe game.

### Reference

- Minimax
    - https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
    - http://programmermagazine.github.io/201407/htm/focus3.html)
    - https://web.cs.ucla.edu/~rosen/161/notes/minimax.html
- Alpha-beta pruning
    - http://web.cs.ucla.edu/~rosen/161/notes/alphabeta.html

### Troubleshooting

#### CSRF issue

> CSRF_HEADER_NAME¶
>
> Default: 'HTTP_X_CSRFTOKEN'
>
> The name of the request header used for CSRF authentication.
>
> As with other HTTP headers in request.META, the header name received from the server is normalized by converting all characters to uppercase, replacing any hyphens with underscores, and adding an 'HTTP_' prefix to the name. For example, if your client sends a 'X-XSRF-TOKEN' header, the setting should be 'HTTP_X_XSRF_TOKEN'.
>
> Reference: https://docs.djangoproject.com/en/2.2/ref/settings/#csrf-header-name

- use the following code to get token:
  `const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;`
- use the following code to request with the token:
  `axios({headers: {"X-CSRFToken": csrftoken}})`