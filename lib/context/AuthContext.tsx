import { loginTokenPost } from "@/lib/client"
import { client } from "@/lib/client/client.gen"
import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react"

const LOCAL_STORAGE_PRESENT = typeof window !== "undefined"
const LOCAL_STORAGE_KEY = "credential"

type AuthContextType = {
  host: string
  username: string
  password: string
  login: (host: string, username: string, password: string) => Promise<void>
  logout: () => void
}

type AuthContextProps = {
  children: ReactNode
}

const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider = ({ children }: AuthContextProps) => {
  const [host, setHost] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  // Load credential from local storage on mount
  useEffect(() => {
    if (!LOCAL_STORAGE_PRESENT) {
      return
    }
    const existedCredential = window.localStorage.getItem(LOCAL_STORAGE_KEY)
    if (existedCredential) {
      const { host, username, password } = JSON.parse(existedCredential)
      login(host, username, password)
    }
  }, [])

  const login = async (host: string, username: string, password: string) => {
    // Save the old config in case the new one fails
    const oldConfig = client.getConfig()

    // Set the new config
    client.setConfig({ baseURL: host })

    // Try to authenticate with the new config
    try {
      const response = await loginTokenPost({
        client,
        body: { username, password },
      })
      if (response.error) {
        throw new Error("Failed to authenticate")
      }
      if (!response.data) {
        throw new Error("No data returned")
      }
      if (response.data.token_type !== "bearer") {
        throw new Error(`Invalid token type: ${response.data.token_type}`)
      }

      // Save the new config
      setHost(host)
      setUsername(username)
      setPassword(password)

      // Set the new config
      client.setConfig({
        baseURL: host,
        auth: () => response.data.access_token,
      })

      // Save to local storage
      if (LOCAL_STORAGE_PRESENT) {
        localStorage.setItem(
          LOCAL_STORAGE_KEY,
          JSON.stringify({ host, username, password })
        )
      }
    } catch (error) {
      // Restore the old config
      client.setConfig(oldConfig)

      throw error
    }
  }

  const logout = () => {
    setHost("")
    setUsername("")
    setPassword("")
    if (LOCAL_STORAGE_PRESENT) {
      window.localStorage.removeItem(LOCAL_STORAGE_KEY)
    }
  }

  return (
    <AuthContext.Provider value={{ host, username, password, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within a AuthProvider")
  }
  return context
}
