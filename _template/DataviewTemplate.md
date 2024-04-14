# Image Video Grid
```dataviewjs
// 현재 노트의 폴더 경로를 가져옵니다.
const currentFolderPath = this.app.workspace.getActiveFile().parent.path;

// 현재 폴더 내의 .webp 파일만 필터링합니다.
// const jpgFiles = app.vault.getFiles().filter(file => {
//     return (file.extension === 'jpg' || file.extension === 'webm' ) && file.parent.path === currentFolderPath;
// });

// 현재 폴더와 하위 폴더 내의 .webp 파일만 필터링합니다.
const jpgFiles = app.vault.getFiles().filter(file => {
    return (file.extension === 'jpg'
		    || file.extension === 'jpeg'
		    || file.extension === 'png'
		    || file.extension === 'gif'
		    || file.extension === 'mov'
		    || file.extension === 'mp4'
		    || file.extension === 'webp'
		    || file.extension === 'webm')
		    && file.path.startsWith(currentFolderPath);
});

const mycount = 7;

// 10개의 열 헤더 생성
const headers = [];
for (let i = 1; i <= mycount; i++) {
    //headers.push(`File ${i}`);
    headers.push(`❁`);
}

// 테이블 데이터 생성
const rows = [];
for (let i = 0; i < jpgFiles.length; i += mycount) {
    let row = [];
    for (let j = 0; j < mycount; j++) {
        if (i + j < jpgFiles.length) {
            //row.push(jpgFiles[i + j].name);
            if (jpgFiles[i + j].extension === 'jpg'
	            || jpgFiles[i + j].extension === 'jpeg'
	            || jpgFiles[i + j].extension === 'png'
	            || jpgFiles[i + j].extension === 'gif'
	            || jpgFiles[i + j].extension === 'webp') {
	            row.push(dv.paragraph(`![[${jpgFiles[i + j].path}|vid-100px]][🍎](${jpgFiles[i + j].path})`));
	        } else if (jpgFiles[i + j].extension === 'webm') {
	            row.push(dv.paragraph(`![[${jpgFiles[i + j].path}|100]]`));
	        }
        } else {
            row.push("N/A");  // 파일이 없는 경우 "N/A"를 추가
        }
    }
    rows.push(row);
}

// 테이블을 렌더링
dv.table(headers, rows);

```
