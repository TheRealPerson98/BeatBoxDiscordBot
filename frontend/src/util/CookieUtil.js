// util/CookieUtil.js
class CookieUtil {
    /**
     * Fetch roles from cookies that are prefixed with 'role_'
     * @returns {Array} Array of roles fetched from the cookies
     */
    static fetchRolesFromCookies() {
        const roleCookies = document.cookie.split('; ').filter(row => row.startsWith('role_'));
        const fetchedRoles = roleCookies.map(cookie => cookie.split('=')[0].replace('role_', ''));

        return fetchedRoles;
    }
}

export default CookieUtil;
