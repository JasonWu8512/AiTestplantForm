// 创建默认头像的脚本
const fs = require('fs');
const path = require('path');

// 男性头像1 - 蓝色卡通男性
const male1 = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
  <circle cx="50" cy="50" r="50" fill="#4285F4" />
  <circle cx="50" cy="40" r="20" fill="#FFFFFF" />
  <path d="M25,85 C25,65 75,65 75,85" fill="#FFFFFF" />
  <circle cx="42" cy="38" r="3" fill="#333333" />
  <circle cx="58" cy="38" r="3" fill="#333333" />
</svg>
`;

// 男性头像2 - 绿色卡通男性
const male2 = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
  <circle cx="50" cy="50" r="50" fill="#34A853" />
  <circle cx="50" cy="40" r="20" fill="#FFFFFF" />
  <path d="M25,85 C25,65 75,65 75,85" fill="#FFFFFF" />
  <circle cx="42" cy="38" r="3" fill="#333333" />
  <circle cx="58" cy="38" r="3" fill="#333333" />
  <path d="M40,50 C45,55 55,55 60,50" stroke="#333333" stroke-width="2" fill="none" />
</svg>
`;

// 男性头像3 - 橙色卡通男性
const male3 = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
  <circle cx="50" cy="50" r="50" fill="#FBBC05" />
  <circle cx="50" cy="40" r="20" fill="#FFFFFF" />
  <path d="M25,85 C25,65 75,65 75,85" fill="#FFFFFF" />
  <circle cx="42" cy="38" r="3" fill="#333333" />
  <circle cx="58" cy="38" r="3" fill="#333333" />
  <rect x="35" y="30" width="30" height="5" fill="#333333" />
</svg>
`;

// 女性头像1 - 粉色卡通女性
const female1 = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
  <circle cx="50" cy="50" r="50" fill="#FF6B81" />
  <circle cx="50" cy="40" r="20" fill="#FFFFFF" />
  <path d="M25,85 C25,65 75,65 75,85" fill="#FFFFFF" />
  <circle cx="42" cy="38" r="3" fill="#333333" />
  <circle cx="58" cy="38" r="3" fill="#333333" />
  <path d="M40,45 C45,50 55,50 60,45" stroke="#333333" stroke-width="2" fill="none" />
</svg>
`;

// 女性头像2 - 紫色卡通女性
const female2 = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
  <circle cx="50" cy="50" r="50" fill="#9C27B0" />
  <circle cx="50" cy="40" r="20" fill="#FFFFFF" />
  <path d="M25,85 C25,65 75,65 75,85" fill="#FFFFFF" />
  <circle cx="42" cy="38" r="3" fill="#333333" />
  <circle cx="58" cy="38" r="3" fill="#333333" />
  <path d="M42,30 C45,25 55,25 58,30" stroke="#333333" stroke-width="2" fill="none" />
</svg>
`;

// 女性头像3 - 青色卡通女性
const female3 = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
  <circle cx="50" cy="50" r="50" fill="#00BCD4" />
  <circle cx="50" cy="40" r="20" fill="#FFFFFF" />
  <path d="M25,85 C25,65 75,65 75,85" fill="#FFFFFF" />
  <circle cx="42" cy="38" r="3" fill="#333333" />
  <circle cx="58" cy="38" r="3" fill="#333333" />
  <path d="M40,45 C45,40 55,40 60,45" stroke="#333333" stroke-width="2" fill="none" />
</svg>
`;

// 保存SVG文件
const saveAvatar = (content, filename) => {
  const filePath = path.join(__dirname, filename);
  fs.writeFileSync(filePath, content);
  console.log(`Created ${filename}`);
};

// 创建所有头像
saveAvatar(male1, 'male1.svg');
saveAvatar(male2, 'male2.svg');
saveAvatar(male3, 'male3.svg');
saveAvatar(female1, 'female1.svg');
saveAvatar(female2, 'female2.svg');
saveAvatar(female3, 'female3.svg');

console.log('All avatars created successfully!'); 