# Sample Data Files for Testing

This directory contains sample data files to test the Live Commerce Analysis Tool.

## Sample Format Examples

### 1. Streaming Data (streaming_data.csv)
```csv
minute,viewers,likes,comments,clicks
0,100,5,3,1
1,150,12,8,2
2,200,25,15,5
3,180,30,20,8
4,220,45,28,12
5,195,50,25,10
```

### 2. Comments Data (comments_data.csv)
```csv
minute,user,comment
0,user001,こんにちは!
0,user002,楽しみにしてました
1,user003,この商品気になります
1,user004,いくらですか?
2,user005,すごい!欲しい
2,user006,買います!
3,user007,どうやって使うんですか?
3,user008,色は何種類ありますか?
4,user009,ポチりました!
5,user010,ありがとうございました
```

## How to Create Sample Data

### For Streaming Data
Create a CSV/Excel file with columns:
- `minute` or `time`: Time index
- `viewers`: Number of concurrent viewers
- `likes`: Cumulative or per-minute likes
- `comments`: Number of comments
- `clicks`: Number of product clicks

### For Comments Data
Create a CSV/Excel file with columns:
- `minute` or `time`: When the comment was posted
- `user` or `username`: Username (optional)
- `comment`: The actual comment text

### For Video
Use any live commerce video in MP4, MOV, AVI, or MKV format.

## Testing Workflow

1. Prepare your sample files following the formats above
2. Launch the application
3. Upload all three files (video, streaming data, comments data)
4. Click "Analyze" and wait for the results
5. Review the generated report with insights and recommendations
