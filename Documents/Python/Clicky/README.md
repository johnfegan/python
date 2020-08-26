# Clicky
Clicky is a python wrapper for several of the ClickyBounce API endpoints. The tool takes a list [API, ID] followed by the desired paramaters as part of authentication. This is required for all requests. This script exists primarily to simplify this process.

## Basic functionality
ClickyBounce takes data is based on page id rather than URL. This can either be found in an export or retrieved using 

```
import clicky as cb
cbid = cb.getcbid(**[API, ID], url**) 
```

Accessible sites are retrived using:
```
cb.getsites(**[API, ID]**)
```

## Traffic (Site)
Site traffic is retrieved using date format YYYY-MM-DD, siteid and the usual API/ID list. The start and end date range can be a single day up to a maximum period of 100 days.
```
cb.gettraffic(**[API, ID]**, siteid, start, end)
```

By default ClickyBounce reports organic traffic alone, if traffic from all sources is is desired simply pass the number 1 as an additional paramater
```
cb.gettraffic(**[API, ID]**, siteid, start, end, 1)
```

## Traffic (Page)
Page traffic is likewise retrieved using date format YYYY-MM-DD, siteid and the usual API/ID list. The start and end date range can be a single day up to a maximum period of 100 days.

```
cb.getpagetraffic(**[API, ID]**, cbid, start, end)
```

By default ClickyBounce reports organic traffic alone, if traffic from all sources is is desired simply pass the number 1 as an additional paramater
```
cb.getpagetraffic(**[API, ID]**, cbid, start, end, 1)
```

## Keywords by Page (Requires Search Console integration)
```
cb.getkeywords(**[API, ID]**, cbid, start, end)
```

## Authentication for making your own queries
```
cb.getsha(keypair, param)
```