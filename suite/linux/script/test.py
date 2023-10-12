import re
a='wqds[33] DL_MCS_AVG[49342]PUCCH: HARQ_Re'
print(re.findall(r'DL_MCS..*\[(\d+)\]',a))
