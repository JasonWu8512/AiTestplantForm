/**
 * 日期格式化和处理工具函数
 */

/**
 * 格式化日期为指定格式
 * @param {Date|string|number} date 日期对象、时间戳或日期字符串
 * @param {string} format 格式化模板，默认为 'YYYY-MM-DD HH:mm:ss'
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return '';
  
  // 将输入转换为Date对象
  const dateObj = typeof date === 'object' ? date : new Date(date);
  
  // 如果日期无效，返回空字符串
  if (isNaN(dateObj.getTime())) return '';
  
  const year = dateObj.getFullYear();
  const month = String(dateObj.getMonth() + 1).padStart(2, '0');
  const day = String(dateObj.getDate()).padStart(2, '0');
  const hours = String(dateObj.getHours()).padStart(2, '0');
  const minutes = String(dateObj.getMinutes()).padStart(2, '0');
  const seconds = String(dateObj.getSeconds()).padStart(2, '0');
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}

/**
 * 计算时间差，返回"多久前"的友好显示
 * @param {Date|string|number} date 日期对象、时间戳或日期字符串
 * @returns {string} 友好的时间差显示
 */
export function timeAgo(date) {
  if (!date) return '';
  
  // 将输入转换为Date对象
  const dateObj = typeof date === 'object' ? date : new Date(date);
  
  // 如果日期无效，返回空字符串
  if (isNaN(dateObj.getTime())) return '';
  
  const now = new Date();
  const diff = Math.floor((now - dateObj) / 1000); // 时间差（秒）
  
  if (diff < 60) {
    return '刚刚';
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}分钟前`;
  } else if (diff < 86400) {
    return `${Math.floor(diff / 3600)}小时前`;
  } else if (diff < 2592000) {
    return `${Math.floor(diff / 86400)}天前`;
  } else if (diff < 31536000) {
    return `${Math.floor(diff / 2592000)}个月前`;
  } else {
    return `${Math.floor(diff / 31536000)}年前`;
  }
}

/**
 * 获取日期范围的开始和结束时间
 * @param {Array} dateRange 日期范围数组 [startDate, endDate]
 * @returns {Object} 包含开始和结束日期的对象
 */
export function getDateRange(dateRange) {
  if (!dateRange || !Array.isArray(dateRange) || dateRange.length !== 2) {
    return { start: null, end: null };
  }
  
  const [start, end] = dateRange;
  return {
    start: start ? formatDate(start, 'YYYY-MM-DD') : null,
    end: end ? formatDate(end, 'YYYY-MM-DD') : null
  };
} 