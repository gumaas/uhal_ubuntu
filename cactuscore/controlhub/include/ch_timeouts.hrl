%%% ---------------------------------------------------------------------------
%%% @author Robert Frazier
%%%
%%% @since May 2012
%%%
%%% @doc Various timeout parameters (in milliseconds) used within the Control
%%%      Hub
%%% @end
%%% ---------------------------------------------------------------------------

% The timeout (ms) used when waiting for a response from a hardware target.
-define(UDP_RESPONSE_TIMEOUT, 20).

% The timeout (ms) used when waiting for a response from a ch_device_client
% process.  If this timeout is reached, it would generally imply that the
% device client in question has died, or it's so heavily backlogged with
% requests that it's failed to respond in time.
-define(RESPONSE_FROM_DEVICE_CLIENT_TIMEOUT, 600000).

% The time (ms) in which a device client process will shut down if not communicating with board
-define(DEVICE_CLIENT_SHUTDOWN_AFTER, 15000).
