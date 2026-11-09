# anacondaで構築しているので Anaconda Promptで起動する
# streamlit run main.py

import streamlit as st
import numpy as np
import pandas as pd

st.title("Streamlit 入門")
st.write("DataFrame")


#df = pd.DataFrame({
#    '1row' : [1, 2, 3, 4],
#    '2row' : [10, 20, 30, 40],  
#})
#st.dataframe(df.style.highlight_max(axis=0), width=200, height=200)

df = pd.DataFrame(
    np.random.rand(20,3),
    columns=['a','b','c']
)
st.line_chart(df)



"""

### 章
## 節
# 項

```python
import streamlit as st
import numpy as np
import pandas as pd
```


"""

